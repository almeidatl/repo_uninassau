package com.clinicare.AgendaMedica.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.clinicare.AgendaMedica.entity.Consulta;

public interface ConsultaRepository extends JpaRepository<Consulta, Long> {
}