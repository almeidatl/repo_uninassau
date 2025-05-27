package com.clinicare.AgendaMedica.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.clinicare.AgendaMedica.entity.Consulta;
import org.springframework.stereotype.Repository;

@Repository
public interface ConsultaRepository extends JpaRepository<Consulta, Long> {
}