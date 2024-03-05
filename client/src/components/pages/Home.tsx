import React from 'react';
import {isLoggedIn} from '../../assets/jwtAuth'

function Home() {

    const loggedIn = isLoggedIn();
    console.log(loggedIn)

    return (
        <div>
            <h2>This is the home page</h2>
        </div>
    );
}

export default Home;