package com.clinicare.AgendaMedica.repository;

import com.clinicare.AgendaMedica.entity.Paciente;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PacienteRepository extends JpaRepository<Paciente, Long> {}
