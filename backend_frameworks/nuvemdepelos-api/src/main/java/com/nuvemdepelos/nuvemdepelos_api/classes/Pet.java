package com.nuvemdepelos.nuvemdepelos_api.classes;

public class Pet {
    private int id;
    private String nome;
    private String raca;
    private int idade;
    private String sexo;

    public Pet(int id, String name, String raca, int idade, String sexo) {
        this.id = id;
        this.nome = name;
        this.raca = raca;
        this.idade = idade;
        this.sexo = sexo;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getRaca() {
        return raca;
    }

    public void setRaca(String raca) {
        this.raca = raca;
    }

    public int getIdade() {
        return idade;
    }

    public void setIdade(int idade) {
        this.idade = idade;
    }

    public String getSexo() {
        return sexo;
    }

    public void setSexo(String sexo) {
        this.sexo = sexo;
    }
}
