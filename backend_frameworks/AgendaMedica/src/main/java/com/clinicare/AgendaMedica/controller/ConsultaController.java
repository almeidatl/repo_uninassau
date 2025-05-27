package com.clinicare.AgendaMedica.controller;

import com.clinicare.AgendaMedica.entity.Consulta;
import com.clinicare.AgendaMedica.service.ConsultaService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/consultas")
public class ConsultaController {
    @Autowired private ConsultaService consultaService;

    @GetMapping
    public List<Consulta> listarConsultas() {
        return consultaService.listarConsultas();
    }

    @PostMapping
    public Consulta salvarConsulta(Consulta consulta) {
        return consultaService.salvarConsulta(consulta);
    }
}
