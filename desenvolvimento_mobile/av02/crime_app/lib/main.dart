import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: CrimeQuestionScreen(),
    );
  }
}

class CrimeQuestionScreen extends StatefulWidget {
  @override
  _CrimeQuestionScreenState createState() => _CrimeQuestionScreenState();
}

class _CrimeQuestionScreenState extends State<CrimeQuestionScreen> {
  final List<String> questions = [
    "Telefonou para a vítima?",
    "Esteve no local do crime?",
    "Mora perto da vítima?",
    "Devia para a vítima?",
    "Já trabalhou com a vítima?",
  ];
  List<bool> answers = List.filled(5, false);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Interrogatório")),
      body: Center(
        child: Container(
          width: 300,
          height: 500,
          child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Expanded(
              child: ListView.builder(
                itemCount: questions.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text(questions[index]),
                    trailing: Switch(
                      value: answers[index],
                      onChanged: (bool value) {
                        setState(() {
                          answers[index] = value;
                        });
                      },
                    ),
                  );
                },
              ),
            ),
            ElevatedButton(
              onPressed: () {
                int score = answers.where((answer) => answer).length;
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => ResultScreen(score)),
                );
              },
              child: Text("Enviar"),
            ),
          ],
        )
        ),
        
      ),
    );
  }
}

class ResultScreen extends StatelessWidget {
  final int score;
  ResultScreen(this.score);

  String getClassification() {
    if (score == 5) return "Assassino";
    if (score >= 3) return "Cúmplice";
    if (score == 2) return "Suspeita";
    return "Inocente";
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Classificação")),
      body: Center(
        child: Text(
          "Classificação: ${getClassification()}",
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}
