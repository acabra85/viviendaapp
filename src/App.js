import React from 'react'
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/navbar/navbar'
import AllProperties from './pages/navbar/allproperties';
import NewProperty from './pages/navbar/newproperty';
import Countries from "./pages/navbar/countries";

function App() {
    return (
        <Router>
            <NavBar />
            <Routes>
                <Route path='/' element={<AllProperties/>}/>
                <Route path='/newproperty' element={<NewProperty/>}/>
                <Route path='/countries' element={<Countries/>}/>
            </Routes>
        </Router>
    );
}

export default App;
