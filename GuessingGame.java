import java.util.Scanner;
import java.util.Random;
public class GuessingGame{
    public static void main(String[] args) {
        Scanner scanner=new Scanner (System.in);
        Random random=new Random();
        int secretNumber,guess,attempts,round,score;
        do{
             System.out.println("welcome to the GuessingGame");
             System.out.println("enter the lower bound of the range");
              int lowerBound=scanner.nextInt();
             System.out.println("enter the upper bound of the range");
             int upperBound=scanner.nextInt();
              secretNumber=random.nextInt(upperBound-lowerBound+1)+lowerBound;
              attempts=0;
              round=0;
              score=0;
              boolean guessedCorrectly=false;
              while(!guessedCorrectly&&attempts<10){
              System.out.println("enter your guess:");
               guess=scanner.nextInt();
               attempts++;
               if(guess==secretNumber){
              System.out.println("Congratulations!you guessed the number correctly");
              score+=(10-attempts+1);
              guessedCorrectly=true;
              }else if(guess<secretNumber){
              System.out.println("Too low!");
             }else{
             System.out.println("Too high!");
             }
             }
             if(!guessedCorrectly){
              System.out.println("Sorry, you could not guess the number within the given attemts");
             }
                round++;
                System.out.println("your current score:"+score);
              System.out.println("Do you want to play again(yes/no)");
              String playAgain=scanner.next();
              if(!playAgain.equalsIgnoreCase("yes")){
                break;
              }
            }while(true);
            System.out.println("Thanks for playing!");
            scanner.close();
        }
    }