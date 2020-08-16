[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)
[![Run on Repl.it](https://repl.it/badge/github/sarcoma/Invoicing)](https://repl.it/github/sarcoma/Invoicing)
# Invoicing

Console script for producing quotes and invoices from a LaTeX template

![alt text](screenshot.gif "Demonstration")

## Getting Started

Copy .env.example and rename to .env

`cp invoicing/.env.example invoicing/.env`

Copy the example LaTeX invoices

`cp invoicing/templates/Invoice.example.tex invoicing/templates/Invoice.tex`

`cp invoicing/templates/Quote.example.tex invoicing/templates/Quote.tex`

Use `poetry` to install dependencies

`poetry install`

cd into `cd ./invoicing` and run `export DB_FILE=invoicing_local.db && python command_line.py` to begin
