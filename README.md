# AutoCSVAPI
Turns a CSV file into a hacky REST API thing

Uses the titles from the CSV line 0 as query keys. For File:
Name, Age
Alice, 50
Bob, 100
Carlos, 25
Bob, 101

localhost:8888/?Name=Bob&Age=100

or:

localhost:8888/?Name=Bob,Alice

