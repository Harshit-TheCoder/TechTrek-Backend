

[
    {
        "Category": "Sorting",
        "Name": "Bubble Sort Algorithm",
        "Question": "Given an array of N integers, write a program to implement the Bubble Sorting algorithm.",
        "Example": [
        {
            "example": 1,
            "input": "N = 6, array[] = {13, 46, 24, 52, 20, 9}",
            "output": "9, 13, 20, 24, 46, 52",
            "explanation": "After sorting the array is:\n9, 13, 20, 24, 46, 52"
        },
        {
            "example": 2,
            "input": "N = 5, array[] = {5, 4, 3, 2, 1}",
            "output": "1, 2, 3, 4, 5",
            "explanation": "After sorting the array is:\n1, 2, 3, 4, 5"
        }
    ],
    "Code": "#include <bits/stdc++.h>\nusing namespace std;\n\nvoid bubble_sort(int arr[], int n) {\n    // Bubble sort\n    for (int i = n - 1; i >= 0; i--) {\n        for (int j = 0; j <= i - 1; j++) {\n if (arr[j] > arr[j + 1]) {\n int temp = arr[j + 1];\n arr[j + 1] = arr[j];\n arr[j] = temp;\n            }\n        }\n    }\n\n    cout << \"After Using Bubble Sort: \" << \"\\n\";\n    for (int i = 0; i < n; i++) {\n        cout << arr[i] << \" \";\n    }\n    cout << \"\\n\";\n}\n\nint main() {\n    int arr[] = {13, 46, 24, 52, 20, 9};\n    int n = sizeof(arr) / sizeof(arr[0]);\n    cout << \"Before Using Bubble Sort: \" << endl;\n    for (int i = 0; i < n; i++) {\n        cout << arr[i] << \" \";\n    }\n    cout << endl;\n\n    bubble_sort(arr, n);\n    return 0;\n}"
    },

    
]