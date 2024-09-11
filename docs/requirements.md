# Requirements

## Situation

CRECE team needs to retrieve contact data from mailchimp list to identify new persons, locations and prayer requests so they can follow up during the week.
Current situation is they rotate team every week, one or two persons do following tasks:

-   If new person, must download Excel macro from drive, Google drive and Mailchimp credentials.
-   Log in into mailchimp CRECE account and manually download list.
-   Run macro and process data and upload new entries to shared spreadsheet in google drive.
-   Identify new persons and make a list of prayer requests.
-   Call those persons during the week and follow up with prayer requests.
    
    Problems are this has many security and privacy issue as sensitive data is shared with multiple people, including new members.
    Also some persons are not excel expert and have problem running excel macro.

## Task

Help them replace broken excel macro and make it user friendly, if possible automate full task and solve security and privacy issues without incurring into high costs.

## Action

### Iteration 1

First a Tkinter Python cross platform UI was created which replaced Excel macro, process still the same.

### Iteration 2

Second a architecture plan was proposed which includes a lambda triggered weekly which downloads more recent data from mailchimp, process it, creates a report and sends it to CRECE team email address.
Python CLI was extended from GUI code so it can download data from Mailchimp API, generate chart bar reports and sent report via Gmail. Solution is deployed on a Github Runner and triggered weekly.

### Iteration 3

A sentiment analysis is implemented to classify prayer requests into know categories, so prayer can be assigned to CRECE team members according to their expertise.

## Results

### Iteration 1

It was identified that some persons use a old version of Macos which can't run GUI. Also team members are not computer proficient and struggle to download and run the app.

### Iteration 2

Half process is automated and team has more time to focus on calling people. Also POC assured this solution generates no costs.

# Architecture

## C4 Container Diagram

![img](architecture.png)

## C4 Deployment Diagram

![img](deployment.png)

# Backlog

## Write GUI

-   Write Github Actions workflow to build app in Windows and macOs

## Write CLI

-   [X] Write mailchimp connector

-   [X] Write reporting module using jinja2

-   [ ] Write sentiment analysis module POC with scikit

-   [ ] Write email system module

-   [ ] Create dataset and train SVC

## MVP deployed in Github Action Runners

-   [X] Write Github Actions workflow to send email with github action

-   [X] Write Github Actions workflow to trigger workflow weekly

## Lambda Function deployed in AWS

-   [ ] Write terraform module of AWS Lambda and trigger

-   [ ] Write Github Actions workflow to deploy lambda