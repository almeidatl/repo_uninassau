package com.clinicare.AgendaMedica.entity;

import jakarta.persistence.*;

import java.time.LocalDateTime;

@Entity
public class Consulta {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private LocalDateTime data;

    public Consulta(Long id, LocalDateTime data, Paciente paciente) {
        this.id = id;
        this.data = data;
        this.paciente = paciente;
    }

    @ManyToOne
    private Paciente paciente;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public LocalDateTime getData() {
        return data;
    }

    public void setData(LocalDateTime data) {
        this.data = data;
    }

    public Paciente getPaciente() {
        return paciente;
    }

    public void setPaciente(Paciente paciente) {
        this.paciente = paciente;
    }
}
