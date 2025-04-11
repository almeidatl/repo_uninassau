import 'dart:io';

void main() {
  List<String> produtos = [];
  bool continuar = true;

  while (continuar) {
    print('Menu:');
    print('1. Cadastrar produtos');
    print('2. Atualizar produto');
    print('3. Listar produtos');
    print('4. Deletar produto');
    print('5. Sair');
    stdout.write('Escolha uma opção: ');
    String? escolha = stdin.readLineSync();

    switch (escolha) {
      case '1':
        cadastrarProdutos(produtos);
        break;
      case '2':
        atualizarProduto(produtos);
        break;
      case '3':
        listarProdutos(produtos);
        break;
      case '4':
        deletarProduto(produtos);
        break;
      case '5':
        continuar = false;
        print('Programa encerrado.');
        break;
      default:
        print('Opção inválida. Tente novamente.');
    }
  }
}

void cadastrarProdutos(List<String> produtos) {
  while (true) {
    stdout.write('Digite o nome do produto (ou "sair" para voltar ao menu): ');
    String? produto = stdin.readLineSync();
    if (produto == 'sair') {
      break;
    }
    if (produto != null && produto.isNotEmpty) {
      produtos.add(produto);
      print('Produto "$produto" cadastrado com sucesso.');
    } else {
      print('Nome do produto inválido. Tente novamente.');
    }
  }
}

void atualizarProduto(List<String> produtos) {
  listarProdutos(produtos);
  stdout.write('Digite o índice do produto que deseja atualizar: ');
  String? indiceStr = stdin.readLineSync();
  int? indice = int.tryParse(indiceStr ?? '');
  if (indice != null && indice >= 0 && indice < produtos.length) {
    stdout.write('Digite o novo nome do produto: ');
    String? novoProduto = stdin.readLineSync();
    if (novoProduto != null && novoProduto.isNotEmpty) {
      produtos[indice] = novoProduto;
      print('Produto atualizado com sucesso.');
    } else {
      print('Nome do produto inválido. Tente novamente.');
    }
  } else {
    print('Índice inválido. Tente novamente.');
  }
}

void listarProdutos(List<String> produtos) {
  if (produtos.isEmpty) {
    print('Nenhum produto cadastrado.');
  } else {
    print('Produtos cadastrados:');
    for (int i = 0; i < produtos.length; i++) {
      print('$i. ${produtos[i]}');
    }
    print('Total de produtos: ${produtos.length}');
  }
}

void deletarProduto(List<String> produtos) {
  listarProdutos(produtos);
  stdout.write('Digite o índice do produto que deseja deletar: ');
  String? indiceStr = stdin.readLineSync();
  int? indice = int.tryParse(indiceStr ?? '');
  if (indice != null && indice >= 0 && indice < produtos.length) {
    String produtoRemovido = produtos.removeAt(indice);
    print('Produto "$produtoRemovido" deletado com sucesso.');
  } else {
    print('Índice inválido. Tente novamente.');
  }
}