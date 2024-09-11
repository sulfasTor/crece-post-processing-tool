<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#orgheadline10">1. Requirements</a>
<ul>
<li><a href="#orgheadline1">1.1. Situation</a></li>
<li><a href="#orgheadline2">1.2. Task</a></li>
<li><a href="#orgheadline6">1.3. Action</a>
<ul>
<li><a href="#orgheadline3">1.3.1. Iteration 1</a></li>
<li><a href="#orgheadline4">1.3.2. Iteration 2</a></li>
<li><a href="#orgheadline5">1.3.3. Iteration 3</a></li>
</ul>
</li>
<li><a href="#orgheadline9">1.4. Results</a>
<ul>
<li><a href="#orgheadline7">1.4.1. Iteration 1</a></li>
<li><a href="#orgheadline8">1.4.2. Iteration 2</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="#orgheadline13">2. Architecture</a>
<ul>
<li><a href="#orgheadline11">2.1. C4 Container Diagram</a></li>
<li><a href="#orgheadline12">2.2. C4 Deployment Diagram</a></li>
</ul>
</li>
<li><a href="#orgheadline28">3. [ ] Backlog</a>
<ul>
<li><a href="#orgheadline15">3.1. [X] Write GUI <code>[1/1]</code></a>
<ul>
<li><a href="#orgheadline14">3.1.1. [X] Write Github Actions workflow to build app in Windows and macOs</a></li>
</ul>
</li>
<li><a href="#orgheadline21">3.2. [ ] Write CLI <code>[2/4]</code></a>
<ul>
<li><a href="#orgheadline16">3.2.1. [X] Write mailchimp connector</a></li>
<li><a href="#orgheadline17">3.2.2. [X] Write reporting module using jinja2</a></li>
<li><a href="#orgheadline18">3.2.3. [ ] Write sentiment analysis module POC with scikit</a></li>
<li><a href="#orgheadline20">3.2.4. [ ] Write email system module</a></li>
</ul>
</li>
<li><a href="#orgheadline24">3.3. [X] MVP deployed in Github Action Runners <code>[2/2]</code></a>
<ul>
<li><a href="#orgheadline22">3.3.1. [X] Write Github Actions workflow to send email with github action</a></li>
<li><a href="#orgheadline23">3.3.2. [X] Write Github Actions workflow to trigger workflow weekly</a></li>
</ul>
</li>
<li><a href="#orgheadline27">3.4. [ ] Lambda Function deployed in AWS <code>[0/3]</code></a>
<ul>
<li><a href="#orgheadline25">3.4.1. [ ] Write terraform module of AWS Lambda and trigger</a></li>
<li><a href="#orgheadline26">3.4.2. [ ] Write Github Actions workflow to deploy lambda</a></li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
</div>


# Requirements<a id="orgheadline10"></a>

## Situation<a id="orgheadline1"></a>

CRECE team needs to retrieve emails from mailchimp list to identify new persons, locations and prayer requests so they can follow up during the week.
Current situation is they rotate team every week, one or two persons do following tasks:

-   If new person, must download Excel macro from drive, Google drive and Mailchimp credentials.
-   Log in into mailchimp CRECE account and manually download list.
-   Run macro and process data and upload new entries to shared spreadsheet in google drive.
-   Identify new persons and make a list of prayer requests.
-   Call those persons during the week and follow up with prayer requests.
    
    Problems are this has many security and privacy issue as sensitive data is shared with multiple people, including new members.
    Also some persons are not excel expert and have problem running excel macro.

## Task<a id="orgheadline2"></a>

Help them replace broken excel macro and make it user friendly, if possible automate full task and solve security and privacy issues without incurring into high costs.

## Action<a id="orgheadline6"></a>

### Iteration 1<a id="orgheadline3"></a>

First a Tkinter Python cross platform UI was created which replaced Excel macro, process still the same.

### Iteration 2<a id="orgheadline4"></a>

Second a architecture plan was proposed which includes a lambda triggered weekly which downloads more recent data from mailchimp, process it, creates a report and sends it to CRECE team email address.
Python CLI was extended from GUI code so it can download data from Mailchimp API, generate chart bar reports and sent report via Gmail. Solution is deployed on a Github Runner and triggered weekly.

### Iteration 3<a id="orgheadline5"></a>

A sentiment analysis is implemented to classify prayer requests into know categories, so prayer can be assigned to CRECE team members according to their expertise.

## Results<a id="orgheadline9"></a>

### Iteration 1<a id="orgheadline7"></a>

It was identified that some persons use a old version of Macos which can't run GUI. Also team members are not computer proficient and struggle to download and run the app.

### Iteration 2<a id="orgheadline8"></a>

Half process is automated and team has more time to focus on calling people. Also POC assured this solution generates no costs.

# Architecture<a id="orgheadline13"></a>

## C4 Container Diagram<a id="orgheadline11"></a>

![img](architecture.png)

## C4 Deployment Diagram<a id="orgheadline12"></a>

![img](deployment.png)

# [ ] Backlog<a id="orgheadline28"></a>

## [X] Write GUI <code>[1/1]</code><a id="orgheadline15"></a>

### [X] Write Github Actions workflow to build app in Windows and macOs<a id="orgheadline14"></a>

## [ ] Write CLI <code>[2/4]</code><a id="orgheadline21"></a>

### [X] Write mailchimp connector<a id="orgheadline16"></a>

### [X] Write reporting module using jinja2<a id="orgheadline17"></a>

### [ ] Write sentiment analysis module POC with scikit<a id="orgheadline18"></a>

### [ ] Write email system module<a id="orgheadline20"></a>

1.  [ ] Create dataset and train SVC

## [X] MVP deployed in Github Action Runners <code>[2/2]</code><a id="orgheadline24"></a>

### [X] Write Github Actions workflow to send email with github action<a id="orgheadline22"></a>

### [X] Write Github Actions workflow to trigger workflow weekly<a id="orgheadline23"></a>

## [ ] Lambda Function deployed in AWS <code>[0/3]</code><a id="orgheadline27"></a>

### [ ] Write terraform module of AWS Lambda and trigger<a id="orgheadline25"></a>

### [ ] Write Github Actions workflow to deploy lambda<a id="orgheadline26"></a>