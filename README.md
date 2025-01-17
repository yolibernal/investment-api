# Investment API

## Usage

Initialize DB with `pipenv run init_db`

Start API with `pipenv run start`

The `investment_data.json` file has to be places in `/instance` before initializing the DB.

## Routes

* `/`

### Company

* `/company`
  * returns all companies
* `/company/{name}`
  * returns company with {name}
* `/company/{name}/investor`
  * returns all investors in the company with {name}
* `/company/{name}/investment`
  * returns all investments made by company with {name}
  * response format: `{ investments: [...], total: { number_of_investments: x, amount: y } }`

### Investor

Equivalent `company` routes

* `/investor`
* `/investor/{name}`
* `/investor/{name}/company`
* `/investor/{name}/investment`
  * response format: `{ investments: [...], total: { number_of_investments: x, amount_of_rounds: y } }`
  * `amount_of_rounds` is total investment in the investment rounds, not of the investor itself as we don't have data on that

## Investment

* `/investment`
  * returns all investment rounds
* `/investment/{id}`
  * returns investment round with {id}

## DB Schema

Companies and investors are unique by name and city. In investments the city is not specified, so the name identifies the company/investor.
I put the investors from an investment round in a separate table for normalization. Investment rounds are identified by a UUID.

## Comments

Removed duplicate from the dataset

```json
{
  "name": "Zoomlounge",
  "city": "Shiban"
},
```
