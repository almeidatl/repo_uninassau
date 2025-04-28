package com.api.aluno;

public class Aluno {
    private Long id;
    private String nome;
    private String email;
    private double nota;

    public Aluno(Long id, String nome, String email, double nota) {
        this.id = id;
        this.nome = nome;
        this.email = email;
        this.nota = nota;
    }

    // Getters e Setters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public double getNota() {
        return nota;
    }

    public void setNota(double nota) {
        this.nota = nota;
    }
}
