import React from 'react';
import {API} from 'aws-amplify'


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
                "address": payload.address,
                "district": payload.district,
                "area": payload.area,
                "rooms": payload.rooms,
                "price": payload.price,
            }
        ]
    }
}

async function createProperty(payload) {
    let transformedPayload = transform(payload);
    console.log(transformedPayload);
    return await API.post('apivivienda', '/inmueble/new', {
        headers: {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST',
            'Content-Type': 'application/json'
        },
        body: transformedPayload
    });
}

class NewProperty extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            district: 'sasa',
            address: 'sasa',
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
    }

    handleChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;

        this.setState({
            [name]: value
        });
    }

    handleSubmit(event) {
        event.preventDefault();
        createProperty(this.state).then(function (res) {
            alert(JSON.stringify(res));
        });
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
                <input type="submit" value="Submit" />
            </form>
        );
    }
}
export default NewProperty;