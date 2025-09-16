import io
import os
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

# -------------------------------
# Helpers
# -------------------------------

def read_csv_semicolon(path: str) -> pd.DataFrame:
	"""Read CSV using semicolon separator and latin-1 encoding with robust NA handling."""
	return pd.read_csv(
		path,
		sep=';',
		encoding='latin-1',
		na_values=['NULL', '***', '', 'NA', 'N/A', 'NaN'],
		keep_default_na=True,
		low_memory=False,
	)


def to_datetime_br(df: pd.DataFrame, date_col: str, time_col: Optional[str] = None) -> pd.Series:
	"""Parse Brazilian formatted date (dd/mm/yyyy) optionally with time (HH:MM:SS)."""
	if date_col not in df.columns:
		return pd.Series(pd.NaT, index=df.index)
	date_series = df[date_col].astype(str).str.strip()
	if time_col and time_col in df.columns:
		time_series = df[time_col].astype(str).str.strip()
		combined = date_series + ' ' + time_series
		return pd.to_datetime(combined, format='%d/%m/%Y %H:%M:%S', errors='coerce')
	return pd.to_datetime(date_series, format='%d/%m/%Y', errors='coerce')


def coalesce_columns(df: pd.DataFrame, targets: Dict[str, List[str]]) -> pd.DataFrame:
	"""Create target columns by coalescing from a list of candidate columns if present."""
	for target, candidates in targets.items():
		for cand in candidates:
			if cand in df.columns:
				df[target] = df[target].fillna(df[cand]) if target in df.columns else df[cand]
				break
		if target not in df.columns:
			df[target] = pd.NA
	return df


def normalize_key_to_string(df: pd.DataFrame, key: str = "codigo") -> pd.DataFrame:
	"""Coerce merge key to pandas string dtype consistently, via numeric->Int64->string pipeline."""
	if key in df.columns:
		df[key] = pd.to_numeric(df[key], errors='coerce').astype('Int64').astype('string')
	return df


def try_merge(left: pd.DataFrame, right: pd.DataFrame, on_cols: List[str]) -> pd.DataFrame:
	"""Merge if all keys exist; otherwise return left unchanged. Align dtypes to string."""
	if not (all(col in left.columns for col in on_cols) and all(col in right.columns for col in on_cols)):
		return left
	for col in on_cols:
		left[col] = left[col].astype('string')
		right[col] = right[col].astype('string')
	return left.merge(right, on=on_cols, how='left')


def kpi_card(label: str, value) -> None:
	c1, c2 = st.columns([1, 1])
	with c1:
		st.metric(label=label, value=value)


# -------------------------------
# Load data
# -------------------------------
@st.cache_data(show_spinner=False)
def load_data() -> dict:
	data: Dict[str, pd.DataFrame] = {}
	files = {
		"ocorrencia": "ocorrencia.csv",
		"aeronave": "aeronave.csv",
		"ocorrencia_tipo": "ocorrencia_tipo.csv",
		"recomendacao": "recomendacao.csv",
		"fator": "fator_contribuinte.csv",
	}
	for key, fname in files.items():
		if os.path.exists(fname):
			data[key] = read_csv_semicolon(fname)
		else:
			data[key] = pd.DataFrame()
	return data


def prepare_data(d: dict) -> pd.DataFrame:
	occ = d.get("ocorrencia", pd.DataFrame()).copy()
	if not occ.empty:
		# Standardize keys and parse datetime
		occ = coalesce_columns(
			occ,
			{
				"codigo": ["codigo_ocorrencia", "codigo_ocorrencia1", "codigo_ocorrencia2", "codigo_ocorrencia3", "codigo_ocorrencia4"],
				"classificacao": ["ocorrencia_classificacao"],
				"uf": ["ocorrencia_uf"],
				"cidade": ["ocorrencia_cidade"],
				"pais": ["ocorrencia_pais"],
				"aerodromo": ["ocorrencia_aerodromo"],
			}
		)
		occ = normalize_key_to_string(occ, "codigo")
		occ["data_hora"] = to_datetime_br(occ, "ocorrencia_dia", "ocorrencia_hora")
		occ["ano"] = occ["data_hora"].dt.year
		occ["mes"] = occ["data_hora"].dt.to_period("M").astype(str)
		if "ocorrencia_latitude" in occ.columns and "ocorrencia_longitude" in occ.columns:
			occ["latitude"] = pd.to_numeric(occ["ocorrencia_latitude"], errors="coerce")
			occ["longitude"] = pd.to_numeric(occ["ocorrencia_longitude"], errors="coerce")

	air = d.get("aeronave", pd.DataFrame()).copy()
	if not air.empty:
		air = coalesce_columns(
			air,
			{"codigo": ["codigo_ocorrencia2", "codigo_ocorrencia1", "codigo_ocorrencia3", "codigo_ocorrencia4"]}
		)
		air = normalize_key_to_string(air, "codigo")

	otype = d.get("ocorrencia_tipo", pd.DataFrame()).copy()
	if not otype.empty:
		otype = coalesce_columns(otype, {"codigo": ["codigo_ocorrencia1", "codigo_ocorrencia2"]})
		otype = normalize_key_to_string(otype, "codigo")

	rec = d.get("recomendacao", pd.DataFrame()).copy()
	if not rec.empty:
		rec = coalesce_columns(rec, {"codigo": ["codigo_ocorrencia4", "codigo_ocorrencia1", "codigo_ocorrencia2", "codigo_ocorrencia3"]})
		rec = normalize_key_to_string(rec, "codigo")

	fator = d.get("fator", pd.DataFrame()).copy()
	if not fator.empty:
		fator = coalesce_columns(fator, {"codigo": ["codigo_ocorrencia3", "codigo_ocorrencia4", "codigo_ocorrencia1", "codigo_ocorrencia2"]})
		fator = normalize_key_to_string(fator, "codigo")

	# Merge datasets
	base = occ
	otype_ren = otype.rename(columns={"ocorrencia_tipo": "tipo_evento"}) if not otype.empty else otype
	if not otype_ren.empty:
		keep_cols = [c for c in ["codigo", "tipo_evento", "taxonomia_tipo_icao"] if c in otype_ren.columns]
		if keep_cols:
			base = try_merge(base, otype_ren[keep_cols], ["codigo"]).copy()
	if not air.empty:
		air_cols_keep = [c for c in [
			"codigo",
			"aeronave_matricula",
			"aeronave_fabricante",
			"aeronave_modelo",
			"aeronave_tipo_operacao",
			"aeronave_fase_operacao",
			"aeronave_nivel_dano",
			"aeronave_fatalidades_total",
		] if c in air.columns]
		if air_cols_keep:
			base = try_merge(base, air[air_cols_keep], ["codigo"]).copy()
	if not rec.empty:
		rec_counts = rec.groupby("codigo", dropna=False).agg(total_recs=("recomendacao_numero", "nunique")).reset_index()
		rec_counts = normalize_key_to_string(rec_counts, "codigo")
		base = try_merge(base, rec_counts, ["codigo"]).copy()
	if not fator.empty:
		fator_counts = fator.groupby(["codigo"], dropna=False).size().reset_index(name="qtd_fatores")
		fator_counts = normalize_key_to_string(fator_counts, "codigo")
		base = try_merge(base, fator_counts, ["codigo"]).copy()

	return base


# -------------------------------
# UI
# -------------------------------

def sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
	st.sidebar.header("Filtros")
	min_date = pd.to_datetime("2000-01-01")
	max_date = pd.to_datetime(datetime.now().date())
	if "data_hora" in df.columns and df["data_hora"].notna().any():
		min_date = pd.to_datetime(df["data_hora"].min())
		max_date = pd.to_datetime(df["data_hora"].max())
	date_range = st.sidebar.date_input("Período", [min_date.date(), max_date.date()])
	if isinstance(date_range, list) and len(date_range) == 2:
		start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]) + pd.Timedelta(days=1)
		mask_date = (df["data_hora"] >= start) & (df["data_hora"] < end)
	else:
		mask_date = pd.Series(True, index=df.index)

	ufs = sorted([u for u in df.get("uf", pd.Series(dtype=str)).dropna().unique()])
	uf_sel = st.sidebar.multiselect("UF", ufs, default=ufs[:10] if len(ufs) > 0 else [])
	mask_uf = df["uf"].isin(uf_sel) if uf_sel else True

	classes = sorted([c for c in df.get("classificacao", pd.Series(dtype=str)).dropna().unique()])
	class_sel = st.sidebar.multiselect("Classificação", classes, default=classes)
	mask_class = df["classificacao"].isin(class_sel) if class_sel else True

	filtered = df.copy()
	if "data_hora" in filtered.columns:
		filtered = filtered[mask_date]
	if isinstance(mask_uf, pd.Series):
		filtered = filtered[mask_uf]
	if isinstance(mask_class, pd.Series):
		filtered = filtered[mask_class]
	return filtered


def show_kpis(df: pd.DataFrame) -> None:
	c1, c2, c3, c4 = st.columns(4)
	with c1:
		st.metric("Ocorrências", int(df.shape[0]))
	with c2:
		st.metric("Acidentes", int((df.get("classificacao") == "ACIDENTE").sum()))
	with c3:
		st.metric("Incidentes", int((df.get("classificacao") == "INCIDENTE").sum()))
	with c4:
		st.metric("Recomendações", int(df.get("total_recs", pd.Series(0, index=df.index)).fillna(0).sum()))


def section_temporal(df: pd.DataFrame) -> None:
	st.subheader("Série temporal de ocorrências")
	if "mes" not in df.columns:
		st.info("Sem dados de data para série temporal.")
		return
	by_month = df.groupby("mes").size().reset_index(name="ocorrencias").sort_values("mes")
	fig = px.line(by_month, x="mes", y="ocorrencias", markers=True)
	st.plotly_chart(fig, use_container_width=True)


def section_geo(df: pd.DataFrame) -> None:
	st.subheader("Mapa de ocorrências")
	if not {"latitude", "longitude"}.issubset(df.columns):
		st.info("Sem coordenadas para exibir no mapa.")
		return
	geo = df[["latitude", "longitude", "cidade", "uf", "classificacao"]].dropna(subset=["latitude", "longitude"]).copy()
	st.map(geo.rename(columns={"latitude": "lat", "longitude": "lon"}))


def section_categoricals(df: pd.DataFrame) -> None:
	st.subheader("Distribuições categóricas")
	col1, col2 = st.columns(2)
	with col1:
		if "uf" in df.columns:
			by_uf = df.groupby("uf").size().reset_index(name="ocorrencias").sort_values("ocorrencias", ascending=False).head(20)
			fig = px.bar(by_uf, x="uf", y="ocorrencias")
			st.plotly_chart(fig, use_container_width=True)
	with col2:
		if "tipo_evento" in df.columns:
			by_tipo = df.groupby("tipo_evento").size().reset_index(name="ocorrencias").sort_values("ocorrencias", ascending=False).head(20)
			fig = px.bar(by_tipo, x="tipo_evento", y="ocorrencias")
			st.plotly_chart(fig, use_container_width=True)

	col3, col4 = st.columns(2)
	with col3:
		if "aeronave_fabricante" in df.columns:
			by_fab = df.groupby("aeronave_fabricante").size().reset_index(name="ocorrencias").sort_values("ocorrencias", ascending=False).head(15)
			fig = px.bar(by_fab, x="aeronave_fabricante", y="ocorrencias")
			st.plotly_chart(fig, use_container_width=True)
	with col4:
		if "aeronave_modelo" in df.columns:
			by_modelo = df.groupby("aeronave_modelo").size().reset_index(name="ocorrencias").sort_values("ocorrencias", ascending=False).head(15)
			fig = px.bar(by_modelo, x="aeronave_modelo", y="ocorrencias")
			st.plotly_chart(fig, use_container_width=True)


def section_histograms(df: pd.DataFrame) -> None:
	st.subheader("Histogramas")
	cols_num = [
		c for c in ["aeronave_fatalidades_total", "aeronave_assentos", "aeronave_pmd"] if c in df.columns
	]
	if not cols_num:
		st.info("Sem variáveis numéricas disponíveis.")
		return
	col = st.selectbox("Selecione variável numérica", cols_num)
	fig = px.histogram(df, x=col, nbins=30)
	st.plotly_chart(fig, use_container_width=True)


def section_model_image() -> None:
	st.subheader("Modelo de dados")
	img_path = "modelo_dados.webp"
	if os.path.exists(img_path):
		image = Image.open(img_path)
		st.image(image, caption="Modelo lógico fornecido", use_column_width=True)
	else:
		st.info("Imagem do modelo não encontrada.")


# -------------------------------
# App
# -------------------------------

def main():
	st.set_page_config(page_title="Ocorrências Aeronáuticas", layout="wide")
	st.title("Dashboard de Ocorrências Aeronáuticas (CENIPA)")
	#st.caption("Dados carregados de arquivos CSV locais. Codificação latin-1 e separador ';'.")

	data = load_data()
	base = prepare_data(data)
	if base.empty:
		st.warning("Não foi possível carregar dados. Verifique os arquivos CSV.")
		return

	filtered = sidebar_filters(base)
	show_kpis(filtered)
	st.markdown("---")

	section_temporal(filtered)
	st.markdown("---")

	section_geo(filtered)
	st.markdown("---")

	section_categoricals(filtered)
	st.markdown("---")

	section_histograms(filtered)
	st.markdown("---")

	section_model_image()

	with st.expander("Ver amostra dos dados"):
		st.dataframe(filtered.head(100), use_container_width=True)


if __name__ == "__main__":
	main()
