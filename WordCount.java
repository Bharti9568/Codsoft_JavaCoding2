import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.Map;
public class WordCount{
    public static void main(String[] args) {
     Scanner input=new Scanner (System.in);
      String text="";
      System.out.println("Enter a text input or provide a file to count the words:");
        String option=input.nextLine();
        if(option.equalsIgnoreCase("file")){
          System.out.println("Enter the file Path:");
          String filePath=input.nextLine();
          text=readFile(filePath);
        }else{
          System.out.println("Enter the text:");
            text=input.nextLine();
        }
        if(text.isEmpty()){
           System.out.println("No input provided.Exiting Program.");
            return;          
          } 
          String[]words=text.split("[\\s\\p{Punct}]+");
           int wordCount=words.length;
           System.out.print("Total word count"+wordCount);
           System.out.print("\nAdditional features");
           System.out.print("1.Ignoring common words or stop words");
           CountWordsWithStopWords(words);
           System.out.print("\n2.Statistics like the number of unique words or the frequency of each word:");
           calculateWordFrequency(words);
           input.close();
        }
         public static String readFile(String filePath){
         StringBuilder sb= new StringBuilder();
            try{
              File file= new File(filePath);
               Scanner filescanner=new Scanner(file);
            while(fileScanner.hasNextLine()){
                      sb.append(scanner.nextLine());
            }
             scanner.close();
          }
            catch(FileNotFoundException e){
            System.out.print("File not found.Exiting program");
            System.exit(0);
            }
            returnsb.toString();
          }
          public static void CountWordsWithStopWords(String[]words){
            Map<String,Integer>
            wordCountMap=new HashMap<>();
            String[]stopWords={"a","an","the","is","are","of","in","and"};
            for(String word:words){
              if(!isStopWord(word,stopWords)){
                wordCountMap.put(word,wordCountMap.getOrDefault(word,0)+1);
              }
            }
              System.out.print("word count without stop words");
               System.out.print("wordCountMap");
          } 
          public static boolean isStopWord(String word,String[] stopWords){
            for(String stopWord:stopWords){
              if(word.equalsIgnoreCase(stopWord)){
                return true;
              }
            }
              return false;
            }
            public static void calculateWordFrequency(String[]words){
              Map<String,Integer>
              wordFrequencyMap=new HashMap<>();
              for(String word:words){
               wordFrequencyMap.put(word,wordFrequencyMap.getOrDefault(word,0)+1);
              }
              System.out.print("Word frequency:");
              for(Map.Entry<String,Integer>entry:wordFrequencyMap.entrySet()){
               System.out.print(entry.getKey()+":"+entry.getValue());
              }
            }
          }
    