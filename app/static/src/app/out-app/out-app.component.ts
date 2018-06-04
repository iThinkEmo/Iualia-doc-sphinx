import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-out-app',
  templateUrl: './out-app.component.html',
  styleUrls: ['./out-app.component.css']
})
export class OutAppComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  openTerms() {
    window.open("https://seller.pakke.mx/#/aviso-de-privacidad");
  }


}
