import $ from 'jquery';
import React from 'react';

function getCountryList() {
    const q = $.Deferred();
    $.get('https://restcountries.com/v3.1/all', function (data) {
        let filtered =  data.map((c) => {
            const name = c.name.common;
            const code = c.cca3;
            const capital = c.capital && c.capital.length > 0 ? (c.capital[0] + ',') : '';
            return {
                key: code,
                val: capital + name
            };
        });
        q.resolve(filtered);
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
                countries.set(e.key, e.val);
                countriesList.push({
                    code: e.key,
                    name: e.val
                });
            });
            countriesList.sort((a,b) => a.name < b.name ? -1 : (a.name > b.name ? 1 : 0));
            countriesList.unshift({code:'COL', name:'Bogota,Colombia'});
            countriesList.unshift({code:'_', name:' -Seleccione- '});
            _ref.setState({
                name: countries.get('_'),
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
            name: countries.get(value),
            code: value
        });
        this.props.onSelectCountry(value);
    }
    render() {
        if(countries.size > 1) {
            return <select name="code" value={this.state.code} onChange={this.handleChange}>
                {this.renderCountryOptions(countriesList)}
            </select>;
        }
        return <select name="code" value={this.state.code} onChange={this.handleChange}>
            <option value="_"> -Seleccione- </option>
            <option value="COL">Bogota,Colombia</option>
        </select>;
    }

    renderCountryOptions(countriesList) {
        return countriesList.map((country) => <option value={country.code}>{country.name}</option>)
    }
}

export default Countries;