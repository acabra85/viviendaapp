import React from 'react';
import {API} from 'aws-amplify'
import Countries from "./countries";

function transform(payload) {
    return {
        "owner": {
            "id": payload.owner_id,
            "name": payload.owner_name,
            "phone_number": payload.owner_phone,
            "email": payload.owner_email
        },
        "properties" : [
            {
                "address": payload.address + ',' + payload.country,
                "district": payload.district,
                "area": payload.area,
                "rooms": payload.rooms,
                "price": payload.price,
            }
        ]
    }
}

async function createProperty(payload) {
    return await API.post('apivivienda', '/inmueble', {
        headers: {
            'Content-Type': 'application/json'
        },
        body: transform(payload)
    });
}

class NewProperty extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.state = {
            district: '_',
            address: 'sasa',
            country: '',
            price: 10,
            rooms: 3,
            area: 20,
            owner_id: '111',
            owner_name: 'dasdsa',
            owner_phone: '31312321',
            owner_email: 'adasda@gmail.com'
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleCountryChange = this.handleCountryChange.bind(this);
    }

    handleChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;

        this.setState({
            [name]: value
        });
    }

    handleCountryChange(code) {
        this.setState({
            country: code
        });
    }

    handleSubmit(event) {
        let elementById = document.getElementById('submit_registration_btn');
        elementById.disabled = true;
        event.preventDefault();
        createProperty(this.state).then(function (res) {
            alert('registration created: ' + JSON.stringify(res));
        })
        .finally(() => elementById.disabled = false)
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <h2>Datos del Propietario</h2><br/>
                <label>
                    Numero Identificacion:
                    <input type="number" name="owner_id" value={this.state.owner_id} onChange={this.handleChange} required/>
                </label><br />
                <label>
                    Nombre Completo:
                    <input type="text" name="owner_name" value={this.state.owner_name} onChange={this.handleChange} required/>
                </label><br />
                <label>
                    Numero de Telefono:
                    <input type="number" name="owner_phone" value={this.state.owner_phone} onChange={this.handleChange} required/>
                </label><br />
                <label>
                    e-mail:
                    <input type="email" name="owner_email" value={this.state.owner_email} onChange={this.handleChange} required/>
                </label><br />
                <h2>Datos del Inmueble</h2><br/>
                <label>
                    Direccion:
                    <input type="text" name="address" value={this.state.address} onChange={this.handleChange} required/>
                </label><br />
                <label>
                    Pais, Ciudad:
                    <Countries onSelectCountry={this.handleCountryChange}/>
                </label><br />
                <label>
                    Localidad:
                    <input type="text" name="district" value={this.state.district} onChange={this.handleChange} required/>
                </label><br />
                <label>
                    Precio:
                    <input type="number" name="price" min="1" value={this.state.price} onChange={this.handleChange} required/>
                </label><br />
                <label>
                    Numero de Habitaciones:
                    <input type="number" name="rooms" min="1" value={this.state.rooms} onChange={this.handleChange} required/>
                </label><br />
                <label>
                    Area (m2):
                    <input type="number" name="area" min="1" value={this.state.area} onChange={this.handleChange} required/>
                </label><br />
                <input type="submit" id="submit_registration_btn" value="Registrar" />
            </form>
        );
    }
}
export default NewProperty;