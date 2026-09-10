# Module 2c: Creating the Add Form
<!-- vscode-markdown-toc -->
1. [Preliminaries](#1-preliminaries)
2. [Update Database](#2-update-database)
3. [Instructions](#3-instructions)
4. [Reports Module](#4-reports-module)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->
## 1. Preliminaries

For this module, the report generation feature will be added to the application. More specifically, the following should
be added to your respective applications by the end of this case:

* Generate informative figure and list of movie details
* Filter the generated list of movie details
* Filter information to be shown in the figure

At this point, it is encouraged that you continue your work from the previous case.
Note: All variable/database names are only suggestions. Since you are new to this, it is suggested that you copy them for
now. Changing the names for your own app is a double-edged sword – it forces you to understand how the app works on
a deeper level but also, implementation on your end can be more difficult

## 2. Update Database

For this module, we will work with four tables: movies, genres, countries, and actors. Refer to the relational model below.


<img width="776" height="490" alt="image" src="https://github.com/user-attachments/assets/ebc07685-55d3-4559-8149-013740049162" />

Insert dummy data for you to appreciate the figure and table that we are going to generate

## 3. Instructions

* Create the **reports folder** inside the apps folder. This will contain all files related to generating reports.
* Copy the **report.py** file and paste it into the **reports folde**r.
* Update your **index and commonmodules** files to accommodate the report module. Note: the href of the report module is **‘/reports/report’**.

## 4. Reports Module
Go ahead and run the app! The report module should look like this.

<img width="911" height="437" alt="image" src="https://github.com/user-attachments/assets/f46b801d-51e7-4d19-89dc-2cc94c09893c" />

Study how the code works! This case will help you in building your app for your project. Try to improve the layout. Happy coding! Good luck! 

