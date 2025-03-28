import 'package:flutter/material.dart';

void main() {
  runApp(ProdutoApp());
}

class ProdutoApp extends StatelessWidget {
  const ProdutoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Gestão de Produtos',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: ProdutoScreen(),
    );
  }
}

class ProdutoScreen extends StatefulWidget {
  const ProdutoScreen({super.key});

  @override
  _ProdutoScreenState createState() => _ProdutoScreenState();
}

class _ProdutoScreenState extends State<ProdutoScreen> {
  List<String> produtos = [];
  final TextEditingController _produtoController = TextEditingController();

  void _cadastrarProduto() {
    if (_produtoController.text.isNotEmpty) {
      setState(() {
        produtos.add(_produtoController.text);
      });
      _produtoController.clear();
    }
  }

  void _atualizarProduto(int index) {
    _produtoController.text = produtos[index];
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Atualizar Produto'),
          content: TextField(controller: _produtoController),
          actions: [
            TextButton(
              onPressed: () {
                if (_produtoController.text.isNotEmpty) {
                  setState(() {
                    produtos[index] = _produtoController.text;
                  });
                }
                _produtoController.clear();
                Navigator.of(context).pop();
              },
              child: Text('Salvar'),
            ),
          ],
        );
      },
    );
  }

  void _deletarProduto(int index) {
    setState(() {
      produtos.removeAt(index);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Gestão de Produtos')),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _produtoController,
              decoration: InputDecoration(labelText: 'Nome do Produto'),
            ),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: _cadastrarProduto,
              child: Text('Cadastrar Produto'),
            ),
            Expanded(
              child: ListView.builder(
                itemCount: produtos.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text(produtos[index]),
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        IconButton(
                          icon: Icon(Icons.edit),
                          onPressed: () => _atualizarProduto(index),
                        ),
                        IconButton(
                          icon: Icon(Icons.delete),
                          onPressed: () => _deletarProduto(index),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
