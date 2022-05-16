import $ from 'jquery';
import React from 'react';

const _mockCountryData = [
    {name: {common: 'Colombia'}, cca3: 'COL', capital: ['Bogota']},
    {name: {common: 'United Arab Emirates'}, cca3: 'UAE', capital: ['Dubai']},
    {name: {common: 'Poland'}, cca3: 'POL', capital: ['Warsaw']},
];
const OFFLINE = true;

function filterRawCountryData(data) {
    return data.map((c) => {
        const name = c.name.common;
        const code = c.cca3;
        const capital = c.capital && c.capital.length > 0 ? (', ' + c.capital[0]) : '';
        const _capital = c.capital && c.capital.length > 0 ? (c.capital[0] + ', ') : '';
        return {
            key: code,
            val: name + capital,
            capitalCountry: _capital + name,
            sortBy: name
        };
    });
}

function getCountryList(obj) {
    const q = $.Deferred();
    if(OFFLINE) {
        q.resolve(filterRawCountryData(_mockCountryData));
        return q;
    }
    $.get('https://restcountries.com/v3.1/all', function (data) {
        q.resolve(filterRawCountryData(data));
    }).fail(function () {
        q.resolve([]);
    });
    return q;
}
const countries = new Map();
const countriesList = []
countries.set('_', ' -Seleccione- ');

class Countries extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.state = {
            name: ' -Seleccione- ',
            code: '_'
        }
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        const _ref = this;
        getCountryList(_ref).then(function(res) {
            countriesList.length = 0;
            res.forEach(e => {
                countries.set(e.key, e);
                countriesList.push({
                    code: e.key,
                    name: e.val,
                    sortBy: e.sortBy
                });
            });
            countriesList.sort((a,b) => a.sortBy < b.sortBy ? -1 : (a.sortBy > b.sortBy ? 1 : 0));
            if (!OFFLINE) {
                countriesList.unshift({code: 'COL', name: 'Colombia, Bogota', sortBy: 'Colombia'});
            }
            countriesList.unshift({code:'_', name:' -Seleccione- '});
            _ref.setState({
                name: countries.get('_').val,
                code: '_'
            });
        });
    }

    handleSubmit(event) {
        event.preventDefault();
    }

    handleChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        this.setState({
            name: countries.get(value).val,
            code: value
        });
        this.props.onSelectCountry(countries.get(value).capitalCountry);
    }
    render() {
        if(countries.size > 1) {
            return <select name="code" value={this.state.code} onChange={this.handleChange}>
                {this.renderCountryOptions(countriesList)}
            </select>;
        }
        return <select name="code" value={this.state.code} onChange={this.handleChange}>
            <option value="_"> -Seleccione- </option>
        </select>;
    }

    renderCountryOptions(countriesList) {
        return countriesList.map((country) => <option value={country.code}>{country.name}</option>)
    }
}

export default Countries;