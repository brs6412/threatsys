import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Iocs } from './iocs';

describe('Iocs', () => {
  let component: Iocs;
  let fixture: ComponentFixture<Iocs>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Iocs]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Iocs);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
