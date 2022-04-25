# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 21:08:44 2022

@author: siri namburi
"""

import unittest
from datetime import datetime,timedelta
from random import randint


import app as AFI_UI

class TestEndtoEnd(unittest.TestCase):

    def setUp(self):
       AFI_UI.app.testing = True
       self.app = AFI_UI.app.test_client(self)
       self._register_details()

    def _register_details(self):
        try:
            response = self.app.post('/login',
                data = dict(Username='test',password='test')
                )
            assert response.status_code == 200

        except:
            response = self.app.post('/signup',
            data = dict(Username='test',email='test@gmail.com',password = 'test',password2='test'))
        
            assert response.status_code == 200


    def testlogin(self):
        response = self.app.post('/login',
            data = dict(Username="test", password="test"))
        assert response.status_code==200
       
    def test_home_page(self):
        response = self.app.get("/")
        assert response.status_code == 200        
    
    def test_tank_input_form(self):

        response = self.app.post('/tankinput',
            data= dict(tank_name='tstcir'+str(randint(0,1000000)),
                TANK='circle',
                diameter=1,cheight=1))

        assert response.status_code == 200

        response = self.app.post('/tankinput',
            data= dict(tank_name='tstrec'+str(randint(0,1000000)),TANK='rectangle',
                length=1,depth=1,width=1))
        assert response.status_code == 200

        response = self.app.post('/tankinput',
            data= dict(tank_name='tstnorm'+str(randint(0,1000000)),
                top1=1,top2=1,base1=1,base2=1,height=1))
        assert response.status_code == 200

    def test_rainfall_input(self):
        response = self.app.post('/rainfallinput',
            data = dict(date=datetime.today().date(),rainfall = 1) 
            )
        assert response.status_code==200

    def test_irrigation_schedule(self):
        response = self.app.post('/irrigationschedule',
            data = dict(start_date=[datetime.today().date()]*3,
                start_time = [datetime.now()]*3,
                end_time =[datetime.now()+timedelta(minutes=1)]*3 ,
                frequency=[1]*3,

                )

            )
        assert response.status_code==200




if __name__ == '__main__':
    unittest.main()