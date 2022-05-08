import React from 'react';
import {API} from 'aws-amplify'

async function getProperties(filterProps) {
    let qParams = '?asc=' + filterProps.asc + '&rows=' + filterProps.rows + '&filterColumn='+filterProps.filter_column;
    return await API.get('apivivienda', '/inmuebles' + qParams, {
        headers: {
            'Content-Type': 'application/json'
        }
    });
}

class AllProperties extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            rows: 10,
            filter_column: 'district',
            asc: false,
            rs_properties: []
        }
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    renderPropertiesTable() {
        return this.state.rs_properties.map((p) => {
            return <tr>
                <td>{p.address}</td>
                <td>{p.district}</td>
                <td>{p.area}</td>
                <td>{p.rooms}</td>
                <td>{p.price}</td>
            </tr>;
        })
    }

    handleSubmit(event) {
        event.preventDefault();
    }

    handleChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;
        this.setState({
            [name]: name === 'asc' ? value === 'true' : value
        });
    }

    render() {
        const name = 'rs_properties';
        this.setState({
            [name]: getProperties(this.state)
        });
        return (
            <div>
                <h3>Todos los Inmuebles</h3>
                <div>
                    <form onSubmit={this.handleSubmit}>
                        <label>
                            Resultados:
                            <select name="rows" value={this.state.rows} onChange={this.handleChange}>
                                <option value="10">10</option>
                                <option value="50">50</option>
                                <option value="100">100</option>
                            </select>
                        </label>
                        <label>
                            Filtro:
                            <select name="filter_column" value={this.state.filter_column} onChange={this.handleChange}>
                                <option value="district">Localidad</option>
                                <option value="registration_date">Fecha Creacion</option>
                            </select>
                        </label>
                        <label>
                            Orden:
                            <select name="asc" value={this.state.asc} onChange={this.handleChange}>
                                <option value="true">Ascendente</option>
                                <option value="false">Descendente</option>
                            </select>
                        </label>
                    </form>
                </div>
                <div>
                    {this.renderPropertiesTable()}
                </div>
            </div>
        );
    }
}
export default AllProperties;
