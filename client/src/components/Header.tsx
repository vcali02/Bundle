import React, {useState, useEffect} from 'react';
import {Nav, Navbar, Container} from "react-bootstrap"
import {Link} from "react-router-dom"
import {isLoggedIn, removeToken} from '../assets/jwtAuth'
import {confirmAlert} from 'react-confirm-alert'

function Header() {

    const loggedIn = isLoggedIn();
    console.log(loggedIn)

    const handleLogout = () => {
        confirmAlert({
            title: 'Confirm Logout',
            message: 'Are you sure you want to logout?',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => {
                        removeToken();
                    }
                },
                {
                    label: 'No',
                }
            ]
        })
    }

    return (
        <Navbar expand="lg">
            <Container>
                {loggedIn ? (
                    <>
                    <Navbar.Brand>
                    <Link to="/">
                        <h2>Bundle</h2>
                    </Link>
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="custom-header justify-content-end">
                        <Nav.Link as={Link} to="/" onClick={handleLogout}>Log Out</Nav.Link>

                    </Nav>
                </Navbar.Collapse>
                    </>
                ) : (
                <>
                <Navbar.Brand>
                    <Link to="/">
                        <h2>Bundle</h2>
                    </Link>
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="custom-header justify-content-end">
                        <Nav.Link as={Link} to="/signup">Sign Up</Nav.Link>
                        <Nav.Link as={Link} to="/login">Login</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
                </>
                )}
                
            </Container>
        </Navbar>
    );
}

export default Header;