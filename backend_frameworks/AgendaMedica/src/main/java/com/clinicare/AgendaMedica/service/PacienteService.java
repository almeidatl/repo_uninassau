package com.clinicare.AgendaMedica.service;

import com.clinicare.AgendaMedica.entity.Paciente;
import com.clinicare.AgendaMedica.repository.PacienteRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PacienteService {

    @Autowired
    private PacienteRepository pacienteRepository;

    public List<Paciente> listarPacientes() {
        return pacienteRepository.findAll();
    }

    public Paciente salvarPaciente(Paciente paciente) {
        return pacienteRepository.save(paciente);
    }

}
