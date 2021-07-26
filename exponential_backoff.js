const delay = ms => new Promise(resolve => setTimeout(resolve, ms))
await delay(1000)

export function faultTolerantCall<T>(call: () => Promise<T>, retryOptions?: Partial<IBackOffOptions>): Promise<T> {
    const retryDefaults: Partial<IBackOffOptions> = {
        delayFirstAttempt: false,
        numOfAttempts: 5,
        jitter: JitterTypes.Full,
        startingDelay: 100,
        timeMultiple: 1.5,
    };
    return backOff(call, Object.assign(retryDefaults, retryOptions || {}));

