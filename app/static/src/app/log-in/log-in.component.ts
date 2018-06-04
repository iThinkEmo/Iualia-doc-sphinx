import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';
import { PasswordValidation } from './validators/password-validator';

@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.scss']
})
export class LogInComponent implements OnInit {

  logInForm: FormGroup;
  registerForm: FormGroup;

  constructor(
    private _formBuilder: FormBuilder,
  ) {

  }

  ngOnInit() {
    // initiates the basic data form and its validators
    this.logInForm = this._formBuilder.group({
        email    : ['', Validators.compose([Validators.required, Validators.email])],
        password : ['', Validators.required],
      });

    this.registerForm = this._formBuilder.group({
        name           : ['', [Validators.required, Validators.pattern("[a-zA-Z ]*")]],
        email          : ['', Validators.compose([Validators.required, Validators.email])],
        password       : ['', [Validators.required, Validators.minLength(8)]],
        confirmPassword: ['', [Validators.required]]
      },{
        validator: PasswordValidation.MatchPassword
    });
  }



}
