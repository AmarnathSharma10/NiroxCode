import java.util.Scanner;

public class Main {

    // Function to perform binary search
    public static int binarySearch(int[] array, int target) {
        int left = 0;
        int right = array.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            // Check if target is present at mid
            if (array[mid] == target) {
                return mid; // Target found
            }

            // If target is greater, ignore the left half
            if (array[mid] < target) {
                left = mid + 1;
            }
            // If target is smaller, ignore the right half
            else {
                right = mid - 1;
            }
        }

        // Target is not present in the array
        return -1;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Input array size
        System.out.print("Enter the number of elements in the array: ");
        int n = scanner.nextInt();

        // Input array elements
        int[] array = new int[n];
        System.out.println("Enter the elements of the array (sorted): ");
        for (int i = 0; i < n; i++) {
            array[i] = scanner.nextInt();
        }

        // Input target element
        System.out.print("Enter the target element: ");
        int target = scanner.nextInt();

        // Perform binary search
        int result = binarySearch(array, target);

        // Output the result
        if (result == -1) {
            System.out.println("Element not present in the array");
        } else {
            System.out.println("Element found at index " + result);
        }

        scanner.close();
    }
}