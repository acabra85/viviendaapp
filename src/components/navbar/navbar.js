import React from 'react';
import {Link} from "react-router-dom";

const NavBar = () => {
    return (
        <div>
            <li>
                <Link to="/">Todos los Inmuebles</Link>
            </li>
            <li>
                <Link to="/newproperty">Nuevo Inmueble</Link>
            </li>
            <li>
                <Link to="/countries">Paises</Link>
            </li>
        </div>
    );
}
export default NavBar;