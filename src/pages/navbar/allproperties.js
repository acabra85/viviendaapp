import React from 'react';
import {API} from 'aws-amplify'

async function getProperties(page, pageSize, filterColumn, asc) {
    let qParams = ''
        + '?page=' + page
        + '&pageSize=' + pageSize
        + '&filterColumn=' + filterColumn
        + '&asc=' + asc;
    return await API.get('apivivienda', '/inmuebles' + qParams, {
        headers: {
            'Content-Type': 'application/json'
        }
    });
}

async function deletePropertyRequest(propertyId) {
    return await API.del('apivivienda', '/inmueble/' + propertyId, {
        headers: {
            'Content-Type': 'application/json'
        }
    });
}

class AllProperties extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            pageSize: 10,
            filterColumn: 'district',
            asc: true,
            page_number: 1,
            totalPages: 1,
            data: null
        }
        const _ref = this;
        getProperties(this.state.page_number, this.state.pageSize, this.state.filterColumn, this.state.asc)
            .then(function(res) {
                if (res && 'success' === res.result) {
                    _ref.setState({
                        totalPages: 1 * res.totalRecords / _ref.state.pageSize,
                        data: res.records
                    });
                }
            });
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    deleteProperty(propertyId) {
        deletePropertyRequest(propertyId).then(
            function (res) {
                if(res && 'success' === res.result) {
                    alert('Propiedad Eliminada!!');
                } else {
                    alert('Error, intentar nuevamente');
                }
            }
        )
    }

    renderPropertiesTable(properties) {
        return properties.map((p) => {
            return <tr>
                        <td>{p.address}</td>
                        <td>{p.district}</td>
                        <td>{p.area}</td>
                        <td>{p.rooms}</td>
                        <td>{p.price}</td>
                        <td>{p.registeredOn}</td>
                        <td>{p.ownerName}</td>
                        <td>{p.ownerId}</td>
                        <td>{p.ownerEmail}</td>
                        <td>{p.ownerPhone}</td>
                        <td>
                            <button type="button" onClick={() => this.deleteProperty(p.id)} >
                                Borrar
                            </button>
                        </td>
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
        let page = name==='page' ? value : this.state.page_number;
        let pageSize = name==='pageSize' ? value : this.state.pageSize;
        let filterColumn = name==='filterColumn' ? value : this.state.filterColumn;
        let asc = name === 'asc'? value === 'true' : this.state.asc;
        const _ref = this;
        getProperties(page, pageSize, filterColumn, asc)
            .then(function(res) {
                if (res && 'success' === res.result) {
                    _ref.setState({
                        totalPages: 1 * res.totalRecords / pageSize,
                        data: res.records
                    });
                }
            })
    }

    render() {
        return (
            <div>
                <h3>Todos los Inmuebles</h3>
                <div>
                    <form onSubmit={this.handleSubmit}>
                        <label>
                            Resultados:
                            <select name="pageSize" value={this.state.pageSize} onChange={this.handleChange}>
                                <option value="5">5</option>
                                <option value="10">10</option>
                                <option value="20">20</option>
                            </select>
                        </label>
                        <label>
                            Filtro:
                            <select name="filterColumn" value={this.state.filterColumn} onChange={this.handleChange}>
                                <option value="district">Localidad</option>
                                <option value="registeredOn">Fecha Creacion</option>
                            </select>
                        </label>
                        <label>
                            Orden:
                            <select name="asc" value={this.state.asc} onChange={this.handleChange}>
                                <option value="true">Ascendente</option>
                                <option value="false">Descendente</option>
                            </select>
                        </label>
                        <label>
                            Pagina:
                            <select name="page" value={this.state.page} onChange={this.handleChange}>
                                {this.renderPageOptions()}
                            </select>
                        </label>
                    </form>
                </div>
                <div>
                    <table>
                        <thead>
                            <tr>
                                <td colSpan={6}>Propiedad</td>
                                <td colSpan={4}>Propietario</td>
                                <td>Acciones</td>
                            </tr>
                            <tr >
                                <th>Ciudad</th>
                                <th>Localidad</th>
                                <th>Area (m2)</th>
                                <th>Habitaciones</th>
                                <th>Precio(COP)</th>
                                <th>Fecha Registro</th>
                                <th>Nombre</th>
                                <th>No. Identificacion</th>
                                <th>Email</th>
                                <th>No. Telefono</th>
                                <th>Borrar</th>
                            </tr>
                        </thead>
                        <tbody>
                            {this.state.data ? this.renderPropertiesTable(this.state.data) : <p>Loading ...</p>}
                        </tbody>
                    </table>
                </div>
            </div>
        );
    }

    renderPageOptions() {
        let options = []
        for(let i=0; i<this.state.totalPages;++i) {
            options.push(i+1);
        }
        return options.map(num => <option value={num}>{num}</option>);
    }
}
export default AllProperties;
