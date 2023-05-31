import React from "react";

function SearchBar({setCompany}) {
    const handleEnter = (e) => {
        if (e.key === 'Enter') {
            //setCompany(e.target.value);
            /* fetch('http://localhost:9999/' + e.target.value)
                .then(response => response.json())
                .then(data => console.log(data)) */
            fetch('http://localhost:8081/' + e.target.value)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not OK');
                    }
                    else
                        console.log(response);
                        //console.log(response.text());
                        return response.json();
                })
                .then(data => {
                    console.log(data);
                    var d = data[0];
                    setCompany({
                        'name':d.Name,
                        'symbol':d.Symbol,
                        'dayOpen':d.Open,
                        'dayClose':d.Close,
                        'dayHigh':d.High,
                        'dayLow':d.Low,
                        'buyRange':'sheeeesh'
                    });
                })
                .catch(error => {
                    console.error('Fetch problem: ', error);
                });
        }
    }

    return(
        <input 
        key="random1"
        placeholder={"Search Company"}
        onKeyDown={handleEnter}
    />
    );
}

export default SearchBar;