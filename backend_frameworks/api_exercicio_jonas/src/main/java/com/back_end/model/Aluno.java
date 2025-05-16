package com.back_end.model;

public class Aluno {
    private Long id;
    private String nome;
    private String email;
    private double nota;
    private String endereco;

    public Aluno() {
    }

    public Aluno(Long id, String nome, String email, double nota, String endereco) {
        this.id = id;
        this.nome = nome;
        this.email = email;
        this.nota = nota;
        this.endereco = endereco;
    }

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

    public String getEndereco() {
        return endereco;
    }

    public void setEndereco(String endereco) {
        this.endereco = endereco;
    }

    
}
