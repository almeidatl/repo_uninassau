import 'package:flutter/material.dart';
import '../models/contact.dart';
import 'add_contact_screen.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<Contact> contacts = [];
  List<Contact> filteredContacts = [];
  final _searchController = TextEditingController();

  void _addContact(Contact newContact) {
    setState(() {
      contacts.add(newContact);
      _filterContacts(""); 
    });
  }

  void _filterContacts(String query) {
    setState(() {
      if (query.isEmpty) {
        filteredContacts = contacts;
      } else {
        filteredContacts = contacts.where((contact) {
          return contact.name.toLowerCase().contains(query.toLowerCase()) ||
                 contact.phone.contains(query);
        }).toList();
      }
    });
  }

  @override
  void initState() {
    super.initState();
    _searchController.addListener(() {
      _filterContacts(_searchController.text);
    });
    filteredContacts = contacts;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Agenda de Contatos")),
      body: Column(
        children: [
          Padding(
            padding: EdgeInsets.all(8.0),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                labelText: "Buscar contato...",
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(),
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: filteredContacts.length,
              itemBuilder: (context, index) {
                return ListTile(
                  title: Text(filteredContacts[index].name),
                  subtitle: Text(filteredContacts[index].phone),
                  leading: Icon(Icons.person),
                );
              },
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.add),
        onPressed: () async {
          final newContact = await Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => AddContactScreen()),
          );
          if (newContact != null) {
            _addContact(newContact);
          }
        },
      ),
    );
  }
}