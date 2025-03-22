import java.util.Scanner;

public class ContaBancaria {
    private double saldo = 0;


    public void setSaldo(double saldo) {
        this.saldo = saldo;
    }

    public double getSaldo() {
        return saldo;
    }

    public void depositar(double valor){
        if (valor > 0){
            this.saldo += valor;
        } else {
            System.out.println("Valor inválido");
        }

    }

    public void saque(double valor){
        if (valor <= saldo) {
            this.saldo -= valor;
        } else {
            System.out.println("Saldo insuficiente");
        }
    }

    public static void main(String[] args) {


        ContaBancaria cc01 = new ContaBancaria();

        cc01.setSaldo(20000);

        Scanner entrada = new Scanner(System.in);
        double valor;

        while (true){
            System.out.println("Menu");
            System.out.println("1 - Depositar");
            System.out.println("2 - Sacar");
            System.out.println("3 - Ver saldo");
            System.out.println("4 - Sair");
            System.out.print("Escolha uma opção: ");
            int escolha = entrada.nextInt();

            switch(escolha){
                case 1:
                    System.out.print("Informe o valor a ser depositado: ");
                    valor = entrada.nextDouble();
                    cc01.depositar(valor);
                    break;
                case 2:
                    System.out.print("Informe o valor que deseja sacar: ");
                    valor = entrada.nextDouble();
                    cc01.saque(valor);
                    break;
                case 3:
                    System.out.println("*********************");
                    System.out.printf("  Saldo:$ %.2f  ", cc01.getSaldo());
                    System.out.println("\n*********************");
                    break;
                case 4:
                    System.out.println("********************************************************");
                    System.out.println("  Que sua grana nos renda cada vez mais, volte sempre!  ");
                    System.out.println("********************************************************");
                    entrada.close();
                    return;
                default:
                    System.out.println("**************");
                    System.out.println("Opção inválida");
                    System.out.println("**************");
                    break;
            }


        }
    }
}