package com.back_end.controller;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.back_end.model.Aluno;

@RestController
@RequestMapping("/alunos")
public class AlunoController {

    private List<Aluno> alunos = new ArrayList<>(List.of(
            new Aluno(3L, "Pedro", "pedro@email.com", 5.0, "Rua 1"),
            new Aluno(1L, "João", "joao@email.com", 8.5, "Rua 2"),
            new Aluno(2L, "Maria", "maria@email.com", 10.0, "Rua 3")

    ));

    //    01
    @GetMapping("/bem-vindo/{nome}")
    public String boasVindas(@PathVariable String nome) {
        return "Bem vindo " + nome + "!";
    }

    //    02
    @GetMapping("/aprovados")
    public List<Aluno> getAprovados() {
        List<Aluno> aprovados = new ArrayList<>();
        for (Aluno aluno : alunos) {
            if (aluno.getNota() >= 7.0) {
                aprovados.add(aluno);
            }
        }
        return aprovados;
    }

    //    03
    @GetMapping("/email/{email}")
    public Aluno buscarPorEmail(@PathVariable String email) {
        email = email.toLowerCase();
        for (Aluno aluno : alunos) {
            if (aluno.getEmail().toLowerCase().equals(email)) {
                return aluno;
            }
        }
        return null;
    }

    //      04
    @PutMapping("/{id}/nota")
    public String atualizarNota(@PathVariable Long id, @RequestBody Double nota) {
        for (Aluno aluno : alunos) {
            if (aluno.getId().equals(id)) {
                aluno.setNota(nota);
                return "Nota atualizada com sucesso!";
            }
        }
        return "Aluno não encontrado.";
    }


    //    05
    @DeleteMapping("/{id}")
    public String removerAluno(@PathVariable Long id) {
        for (Aluno aluno : alunos) {
            if (aluno.getId().equals(id)) {
                alunos.remove(aluno);
                return "Aluno removido com sucesso!";
            }
        }
        return "Aluno não encontrado.";
    }

    //    06
    @GetMapping("/ordenados")
    public List<Aluno> listarOrdenados() {
        return alunos.stream()
                .sorted(Comparator.comparing(Aluno::getNome)).toList();
    }

    //    07
    @GetMapping("/media")
    public double calcularMedia() {
        double soma = 0;
        for(Aluno aluno : alunos){
            soma = soma + aluno.getNota();
        }
        return soma / alunos.size();
    }

    //08
    @GetMapping("/quantidade")
    public int quantidadeAlunos() {
        return alunos.size();
    }

    //    09
    @GetMapping("/relatorio")
    public Map<String, Object> gerarRelatorio() {
        Map<String, Object> relatorio = new HashMap<>();
        long aprovados = alunos.stream().filter(a -> a.getNota() >= 7).count();
        long reprovados = alunos.size() - aprovados;

        relatorio.put("total", alunos.size());
        relatorio.put("aprovados", aprovados);
        relatorio.put("reprovados", reprovados);
        relatorio.put("maiorNota", alunos.stream().mapToDouble(Aluno::getNota).max().orElse(0));
        relatorio.put("menorNota", alunos.stream().mapToDouble(Aluno::getNota).min().orElse(0));
        return relatorio;
    }

    public List<Aluno> getAlunos() {
        return alunos;
    }

    public void setAlunos(List<Aluno> alunos) {
        this.alunos = alunos;
    }
}