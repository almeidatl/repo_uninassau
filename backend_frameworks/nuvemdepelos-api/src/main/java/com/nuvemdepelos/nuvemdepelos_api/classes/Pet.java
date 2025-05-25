package com.nuvemdepelos.nuvemdepelos_api.classes;

public class Pet {
    private String name;
    private String raca;
    private int idade;
    private String sexo;

    public Pet(String name, String raca, int idade, String sexo) {
        this.name = name;
        this.raca = raca;
        this.idade = idade;
        this.sexo = sexo;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
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
