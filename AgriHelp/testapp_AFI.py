# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 21:08:44 2022

@author: sindu
"""

import unittest
import app as AFI_UI

class Testapp(unittest.TestCase):

    def setUp(self):
       AFI_UI.app.testing = True
       self.app = AFI_UI.app.test_client()
       
    def test_home_page(self):
        response = self.app.get("/")
        assert response.status_code == 200
            
    def test_registration_form(self):
        response = self.app.get('/signup')
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        # make sure all the fields are included
        assert 'name="Username"' in html
        assert 'name="email"' in html
        assert 'name="password"' in html
        assert 'name="password"' in html
        assert 'name="submit"' in html
    
    def test_login_form(self):
        response = self.app.get('/login')
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        # make sure all the fields are included
        assert 'name="Username"' in html
        assert 'name="password"' in html
        assert 'name="submit"' in html
    
    def test_tank_input_form(self):
        response = self.app.post('/tankinput')
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        # make sure all the fields are included
        assert 'name="tank_name"' in html
        assert 'name="TANK"' in html
        assert 'name="submit"' in html
        assert 'name="cancel"' in html

if __name__ == '__main__':
    unittest.main()