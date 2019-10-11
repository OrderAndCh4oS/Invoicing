[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

# Invoicing

Console script for producing quotes and invoices from a LaTeX template

![alt text](screenshot.gif "Demonstration")

## Getting Started

Copy .env.example and rename to .env

`cp invoicing/.env.example invoicing/.env`

Copy the example LaTeX invoices

`cp invoicing/templates/Invoice.example.tex invoicing/templates/Invoice.tex`

`cp invoicing/templates/Quote.tex invoicing/Quote.tex`

Use `pip` to install dependencies from the `requirements.txt`

`pip install -r requirements.txt`

Run the project from `invoicing/command_line.py` in your ide, this should find all the imports. At least it does in PyCharm.
