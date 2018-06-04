import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OutAppComponent } from './out-app.component';

describe('OutAppComponent', () => {
  let component: OutAppComponent;
  let fixture: ComponentFixture<OutAppComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OutAppComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OutAppComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
