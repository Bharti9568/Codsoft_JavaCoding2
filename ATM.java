import java.util.Scanner;
class BankAccount{
    private double balance;
    public BankAccount(double initialBalance){
        this.balance=initialBalance;
    }
    public double getBalance(){
        return balance;
    }
    public void deposit(double amount){
        balance+=amount;
        System.out.println("Deposit successful:"+balance);
    }
    public void Withdraw(double amount){
        if(balance>=amount){
            balance-=amount;
           System.out.println("Withdrwal successful:"+balance);
        }
        else{
            System.out.println("Insufficient balance");
        }
    }
}
public class ATM
{
    public static void main(String args[] )
    { 
        int balance = 50000, withdraw, deposit;
        Scanner S = new Scanner(System.in);
        while(true)
        {
            System.out.println("welcome to ATM machine ");
            System.out.println("Choose 1 for Withdraw");
            System.out.println("Choose 2 for Deposit");
            System.out.println("Choose 3 for Check Balance");
            System.out.println("Choose 4 for EXIT");
            System.out.print("Choose the operation you want to perform:");
            int n = S.nextInt();
            switch(n)
            {
                case 1:
                System.out.print("Enter money to be withdrawn:");
                withdraw = S.nextInt();
                if(balance >= withdraw)
                {
                    balance = balance - withdraw;
                    System.out.println("Please collect your money");
                }
                else
                {
                    System.out.println("Insufficient Balance");
                }
                System.out.println("");
                break;
                case 2:
                System.out.print("Enter money to be deposited:");
                deposit = S.nextInt();
                balance = balance + deposit;
                System.out.println("Your Money has been successfully depsited");
                System.out.println("");
                break;
                case 3:
                System.out.println("Balance : "+balance);
                System.out.println("");
                break;
                case 4: 
                System. exit(0);
            }
        }    
    }    
}    