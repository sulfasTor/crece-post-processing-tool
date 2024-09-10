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
<li><a href="#orgheadline14">3. Backlog</a></li>
</ul>
</div>
</div>


# Requirements<a id="orgheadline10"></a>

## Situation<a id="orgheadline1"></a>

CRECE team needs to retrieve emails from mailchimp list to identify new persons, location and prayer requests so they can follow up during the week.
Actual situation is they rotate team every week, one persons does the following tasks:

-   If new person, must download Excel macro from drive, Google drive and Mailchimp credentials.
-   Log in into mailchimp CRECE account and manually download list.
-   Run macro and process data and upload new entries to shared spreadsheet in google drive.
-   Identify new persons and make a list of prayer requests.
-   Call those persons during the week and follow up prayer requests.
    
    Problems are this has many security and privacy issue as sensitive data is shared with multiple people, including new members.
    Also some persons are not excel expert and have problem running excel macro.

## Task<a id="orgheadline2"></a>

Help them replace broken excel macro and make it user friendly, if possible automate full task and solve security and privacy issues without incurring into high costs.

## Action<a id="orgheadline6"></a>

### Iteration 1<a id="orgheadline3"></a>

First a Tkinter Python cross platform UI was created which replaced Excel macro, process still the same.

### Iteration 2<a id="orgheadline4"></a>

Second a architecture plan was proposed which includes a lambda triggered weekly which downloads more recent data from mailchimp, process it, creates a report and sends it to CRECE team email address.

### Iteration 3<a id="orgheadline5"></a>

A sentiment analysis is implemented to classify prayer requests into know categories, so prayer can be divided into multiple CRECE team who are akin.

## Results<a id="orgheadline9"></a>

### Iteration 1<a id="orgheadline7"></a>

It was identified that some persons use a old version of Macos which can't run GUI. Also some persons are not computer proficient users and have trouble running app.

### Iteration 2<a id="orgheadline8"></a>

A python CLI was extended from GUI code which can download data from Mailchimp API and generate some chart bar reports and sent via Gmail. Solution is deployed on a Github Runner and trigger weekly.

# Architecture<a id="orgheadline13"></a>

## C4 Container Diagram<a id="orgheadline11"></a>

![img](architecture.png)

## C4 Deployment Diagram<a id="orgheadline12"></a>

![img](deployment.png)

# Backlog<a id="orgheadline14"></a>