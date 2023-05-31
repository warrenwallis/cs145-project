import React, { useState } from 'react';
import MainContent from './MainContent.js';
import SearchBar from './SearchBar.js';

function Window() {
    const [companies, setCompanies] = useState([]);

    const handleNewCompany = (comp) => {
        setCompanies(
            (prev) => {
                let newArr = prev.slice();

                newArr.push(comp);

                return newArr;
            }
        );
    }

    return(
        <div>
            <SearchBar setCompany={handleNewCompany}/>
            <MainContent companies={companies} />
        </div>
    );
}

export default Window;