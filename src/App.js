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


/*

    const [greeting, setGreeting] = useState(null)

    async function getData(path) {
        const data = await API.get('apivivienda', path, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        setGreeting(data.result)
    }

    async function postData(path, payload) {
        const data = await API.post('apivivienda', path, {
            headers: {
                'Content-Type': 'application/json'
            },
            body : payload
        });
        setGreeting(data.result)
    }

    async function deleteData(path) {
        const data = await API.del('apivivienda', path, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        setGreeting(data.result)
    }



    useEffect(() => {
        //postData('/inmueble/new', {})
        deleteData('/inmueble/1/borrar')
        //getData('/inmuebles')
        //getData('/inmueble/1')
        //getData('/propietario/id')
    }, [])

    return (
        <div className="App">
            <header className="App-header">
                <p>
                    Edit <code>src/App.js</code> and save to reload.
                </p>
                <a
                    className="App-link"
                    href="https://reactjs.org"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Learn React
                </a>
                <h1>-[{greeting}]-</h1>
            </header>
        </div>
}
    );*/

