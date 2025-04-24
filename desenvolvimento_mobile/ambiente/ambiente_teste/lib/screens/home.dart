import 'package:flutter/material.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  TextEditingController controlador = TextEditingController();
  String texto = "";
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Usando textEditingController')),
      body: Column(
        children: [
          TextField(
            controller: controlador,
            decoration: InputDecoration(labelText: "Digite algo..."),
          ),
          ElevatedButton(
            onPressed: () {
              setState(() {
                texto = controlador.text;
              });
            },
            child: Text("Mostrar texto"),
          ),
          Text("Texto digitado: $texto"),
        ],
      ),
    );
  }
}
