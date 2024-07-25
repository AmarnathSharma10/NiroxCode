import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        // Create a Scanner object for input
        Scanner scanner = new Scanner(System.in);
        
        // Prompt the user to enter the first number
        
        // Read the first number
        int num1 = scanner.nextInt();
        
        // Prompt the user to enter the second number
       
        // Read the second number
        int num2 = scanner.nextInt();
        
        // Calculate the sum of the two numbers
        int sum = num1 + num2;
        
        // Print the result
        System.out.println(sum);
        
        // Close the scanner
        scanner.close();
    }
}