import React, { useState } from 'react';
import graphPlaceholder from '../images/graphPlaceholder.jpg';

function CompanyInfo(props) {
    return(
        <div className='CompanyInfo'>
            <div><h1>{props.name}</h1></div>
            <div><text>{props.symbol}</text></div>
            <div><h2>Day Open:</h2></div>
            <div><text>{props.dayOpen}</text></div>
            <div><h2>Day Close:</h2></div>
            <div><text>{props.dayClose}</text></div>
            <div><h2>Day High:</h2></div>
            <div><text>{props.dayHigh}</text></div>
            <div><h2>Day Low:</h2></div>
            <div><text>{props.dayLow}</text></div>
            <div>---------</div>
            <div><h2>Buy Range:</h2></div>
            <div><text>{props.buyRange}</text></div>
        </div>
    );
}

function CompanyPrediction({companyInfo}) {
    console.log('companyInfo = ', companyInfo);
    return(
        <div>
            <CompanyInfo
                name={companyInfo.name}
                symbol={companyInfo.symbol}
                dayOpen={companyInfo.dayOpen}
                dayClose={companyInfo.dayClose}
                dayHigh={companyInfo.dayHigh}
                dayLow={companyInfo.dayLow}
                buyRange={companyInfo.buyRange}
            />
            <img className='companyGraph'
                src={graphPlaceholder}
                alt="graph"
            />
        </div>
    );
}

function MainContent({companies}) {
    console.log(companies)
    const renderPredictions = companies.map(
        (comp) => {
            //console.log('comp = ', comp);
            return <CompanyPrediction companyInfo={comp} />
        }
    );

    return (
        <div className='mainContent'>
            {renderPredictions}
        </div>
    ); 
}

export default MainContent;