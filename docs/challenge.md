# Quorum Coding Challenge: Working with Legislative Data

## 📝 Before You Start
Please make sure you read the entire document, including the last section with suggestions, before getting started.

---

## 📊 Overview
At Quorum, we collect and organize a large amount of publicly available government data. For example, we provide our clients the ability to visualize all of the bills that legislators voted for or against.

To represent the data, we designed the database with these models:

- **Person**: An individual legislator elected to government. This includes everyone from President Joe Biden to Representative David McKinley from West Virginia.
- **Bill**: A piece of legislation introduced in the United States Congress.
- **Vote**: A vote on a particular Bill. Bills can be voted on multiple times, as the Bill itself can undergo changes over the course of its life. For this challenge, there will only be up to **1 Vote** provided for each Bill.
- **VoteResult**: A vote cast by an individual legislator for or against a piece of legislation. Each vote cast is associated with a specific Vote.

---

## 📁 Provided Data
You will be provided with a dataset comprised of the following four files:

### `bills.csv`
| Field            | Type     | Description                                      |
|------------------|----------|--------------------------------------------------|
| id               | integer  | The id of the bill                               |
| title            | string   | The name of the bill                             |
| primary_sponsor  | integer  | The id of the primary sponsor (of type Person)   |

### `legislators.csv`
| Field | Type     | Description              |
|-------|----------|--------------------------|
| id    | integer  | The id of the legislator |
| name  | string   | The name of the legislator |

### `votes.csv`
| Field   | Type     | Description                                      |
|---------|----------|--------------------------------------------------|
| id      | integer  | The id of the Vote                               |
| bill_id | integer  | The id of the bill that this vote is associated with |

### `vote_results.csv`
| Field         | Type     | Description                                      |
|---------------|----------|--------------------------------------------------|
| id            | integer  | The id of the VoteResult                         |
| legislator_id | integer  | The id of the legislator casting a vote         |
| vote_id       | integer  | The id of the Vote associated with this cast     |
| vote_type     | integer  | The type of vote cast - `1` for yea, `2` for nay |

---

## 🎯 Task

### Context
Part of our job at Quorum is to transform data into information. This project is about helping a client answer specific questions using our platform.

### Story
As a user, I want to use Quorum to get access to the following information:

1. For every legislator available:
   - How many bills did the legislator support (voted for)?
   - How many bills did the legislator oppose?

2. For every bill available:
   - How many legislators supported the bill?
   - How many legislators opposed the bill?
   - Who was the primary sponsor of the bill?

---

## 🛠 Requirements

1. Build a web application (e.g., Django web application).
2. The goal is to provide the information the client needs.
3. You are free to choose how to display the information. Tables are acceptable, but creativity is encouraged.

### Example Table for Legislator Votes

| ID  | Legislator         | Supported Bills | Opposed Bills |
|-----|--------------------|------------------|----------------|
| 321 | Senator Lorem Ipsum| 1                | 2              |

### Example Table for Bill Votes

| ID  | Bill                        | Supporters | Opposers | Primary Sponsor     |
|-----|-----------------------------|------------|----------|---------------------|
| 123 | BBB 23: Build Brazil Better | 10         | 0        | Rep. Lorem Ipsum    |

---

## 📚 Resources
You will be provided with CSV files containing legislators, bills, votes, and vote results.

---

## ❓ Questions
After completing your implementation, include a write-up answering the following:

1. Discuss your strategy and decisions implementing the application. Consider time complexity, effort cost, technologies used, and other relevant factors.
2. How would you change your solution to account for future columns (e.g., “Bill Voted On Date”, “Co-Sponsors”)?
3. How would you change your solution if instead of receiving CSVs, you were given a list of legislators or bills to generate a CSV for?
4. How long did you spend working on the assignment?

---

## 📦 Submission Instructions
Send a zip file named `your_full_name.zip` containing:

- Source code for your implementation
- A README with steps to run your code (`readme.md`)
- A write-up answering the questions above (`questions.md`)

---

## ✅ Evaluation Criteria

1. **Correctness** – Is your output correct based on the provided data? How did you prove correctness?
2. **Structure/Readability** – Is your code well organized and easy to read? Can it be extended reasonably?
3. **Proficiency with Language** – Does your code follow conventions of your chosen language?

---

## 💡 Suggestions

- Use this test to demonstrate your skills. We evaluate both code quality and decision-making.
- You may use any programming language.
- External libraries (e.g., for parsing CSVs) are allowed. A database is not required.
- Consider using Git to commit your work and show progress.
