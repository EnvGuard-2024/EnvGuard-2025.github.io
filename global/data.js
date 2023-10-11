export const appOptions = [
  { value: 'Temperature regulation effect conflict', label: 'Temperature regulation effect conflict' },
  { value: 'Brightness regulation', label: 'Brightness regulation' },
  { value: 'Raining/Window conflict', label: 'Raining/Window conflict' },
  { value: 'Unsafe use of microwave oven', label: 'Unsafe use of microwave oven' },
  { value: 'Unsafe use of water dispenser', label: 'Unsafe use of water dispenser' },
  { value: 'Excessive humidity', label: 'Excessive humidity' },
  { value: 'Low air quality', label: 'Low air quality' },
  { value: 'Waste of electricity', label: 'Waste of electricity' },
  { value: 'Drinking fountains work too long', label: 'Drinking fountains work too long' },
  { value: 'Excessive noise', label: 'Excessive noise' }
]

export const categoryOptions = [
  { value: 'Time Dependent', label: 'Time Dependent', description: '' },
  { value: 'Time Independent', label: 'Time Independent', description: '' }
]

export const tempTemplateOptions = {
  'Time Dependent': [
    { value: 'event-state-time', label: 'event-state-time', description: 'The [State] [always/never] occur [within/after] the [Time] of the [Event] occurrence.' },
    // { value: 'effect-effect-time', label: 'effect-effect-time', description: 'The Second [Effect] must occur within the [StartTime] ~ [EndTime] of the First [Effect].' },
    { value: 'effect-time', label: 'effect-time', description: 'The execution time of the [Effect] must be [greater than/less than] [Time].' },
    { value: 'one-state', label: 'one-state', description: 'The duration of the [State] must be [greater than/less than] [Time].' },
    // { value: 'one-event', label: 'one-event', description: '[Event] can occur up to [Count] times within [Time].' },
    // { value: 'event-effect-time', label: 'event-effect-time', description: 'The [Effect] cannot occur within the [Time] of the [Event] occurrence.' }
    { value: 'effect-state-time', label: 'effect-state-time', description: 'The [Effect] [always/never] happen [within/after] the [Time] while [state1, ..., staten].' }
  ],
  'Time Independent': [
    { value: 'effect-effect', label: 'effect-effect', description: 'Multiple [effect] [always/never] occur at the same time.' },
    { value: 'state-state', label: 'state-state', description: '[state] should [always/never] be active while [state1, ..., staten].' },
    { value: 'event-state', label: 'event-state', description: '[Event] should [always/never] happen while [state1, ..., staten].' },
    { value: 'effect-state', label: 'effect-state', description: '[effect] should [always/never] happen while [state1, ..., staten].' }
  ]
}

export const symbolOptions = [
  { value: '>', label: '>' },
  { value: '<', label: '<' }
]

export const typeOptions = [
  { value: 'event', label: 'event' },
  { value: 'action', label: 'action' }
]
