import 'package:flutter/material.dart';
import '../models/contact.dart';

class AddContactScreen extends StatefulWidget {
  @override
  _AddContactScreenState createState() => _AddContactScreenState();
}

class _AddContactScreenState extends State<AddContactScreen> {
  final _nameController = TextEditingController();
  final _phoneController = TextEditingController();

  void _submitContact() {
    if (_nameController.text.isNotEmpty && _phoneController.text.isNotEmpty) {
      final newContact = Contact(
        name: _nameController.text,
        phone: _phoneController.text,
      );
      Navigator.pop(context, newContact);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Adicionar Contato")),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _nameController,
              decoration: InputDecoration(labelText: "Nome"),
            ),
            TextField(
              controller: _phoneController,
              decoration: InputDecoration(labelText: "Telefone"),
              keyboardType: TextInputType.phone,
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _submitContact,
              child: Text("Salvar"),
            ),
          ],
        ),
      ),
    );
  }
}